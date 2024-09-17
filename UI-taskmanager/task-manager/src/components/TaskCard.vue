<template>
  <v-card class="task-card">
    <v-card-title>
      <div class="title-container">
        {{ task.subject }}
        <div class="corner-icon-buttons">
          <v-btn icon @click="$emit('open-readonly-task', task)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
          <v-btn icon @click="downloadTask">
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </div>
      </div>
    </v-card-title>
    <v-card-subtitle>
      <div>
        <v-select v-if="!isTaskNotAssignedToCurrentUser" v-model="selectedStatus" :items="statuses" label="Статус"
          @change="updateStatus"></v-select>
      </div>
      <div :class="statusClass">Статус: {{ selectedStatus }}</div>
      <div class="font-weight-bold">
      Приоритет: 
      {{ task.priority }}
      <v-icon :color="priorityIcon.color">{{ priorityIcon.icon }}</v-icon>
    </div>
      <div v-if="assignedToUser">Исполнитель: {{ assignedToUser.name }}</div>
      <div v-if="assignedByUser">Инициатор: {{ assignedByUser.name }}</div>
      <div>Поручение создано: {{ task.registration_date }}</div>
    </v-card-subtitle>
    <v-card-text>
      {{ task.description.length > 30 ? task.description.slice(0, 30) + '...' : task.description }}
    </v-card-text>
    <v-card-actions>
      <v-btn v-if="isTaskNotAssignedToCurrentUser" color="primary" small
        @click="$emit('edit-task', task)">Редактировать</v-btn>
      <v-btn v-if="isTaskNotAssignedToCurrentUser" color="error" small @click="openDeleteDialog">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-card-actions>

    <!-- Диалог для подтверждения удаления -->
    <v-dialog v-model="isDeleteDialogOpen" max-width="400px">
      <v-card>
        <v-card-title class="headline">Подтверждение удаления</v-card-title>
        <v-card-text>Вы уверены, что хотите удалить поручение?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDeleteDialog">Отмена</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    task: {
      type: Object,
      required: true
    },
    users: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      assignedToUser: null,
      assignedByUser: null,
      isTaskNotAssignedToCurrentUser: true,
      isDeleteDialogOpen: false,
      selectedStatus: this.task.status,
      statuses: ['В обработке', 'Завершено', 'Отменено'],
    };
  },
  mounted() {
    this.findAssignedUser();
  },
  methods: {
    async downloadTask() {
      try {

        const token = localStorage.getItem('access_token');

        // Проверяем, что токен существует
        if (!token) {
          throw new Error('Token not found in localStorage');
        }

        // Выполняем запрос с Bearer Token
        const response = await axios.get(`${process.env.VUE_APP_GATEWAY_URL}/documents-api/${this.task.id}/generate-word-document`, {
          responseType: 'blob', // Обработка данных как blob
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        // Проверка заголовка Content-Type
        const contentType = response.headers['content-type'];
        if (contentType !== 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
          throw new Error(`Неправильный тип содержимого: ${contentType}`);
        }

        // Создаем URL для blob объекта
        const url = window.URL.createObjectURL(new Blob([response.data], { type: contentType }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `task_${this.task.id}.docx`);

        // Добавляем ссылку в DOM и выполняем клик
        document.body.appendChild(link);
        link.click();

        // Очищаем после использования
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Ошибка при загрузке файла:', error);
      }
    },
    findAssignedUser() {
      if (this.task.responsible_employee_id) {
        const userId = localStorage.getItem('user_id');

        this.assignedToUser = this.users.find(user => user.id === this.task.responsible_employee_id);
        if (userId == this.assignedToUser.id) {
          this.isTaskNotAssignedToCurrentUser = false;
        }
        const createdByUser = this.users.find(user => user.id === this.task.author_id);
        if ((userId == this.assignedToUser.id) && (userId == createdByUser.id)) {
          this.isTaskNotAssignedToCurrentUser = true;
        }
        if (createdByUser) this.assignedByUser = createdByUser;
      }
    },
    openDeleteDialog() {
      this.isDeleteDialogOpen = true;
    },
    closeDeleteDialog() {
      this.isDeleteDialogOpen = false;
    },
    confirmDelete() {
      this.$emit('delete-task', this.task);
      this.closeDeleteDialog();
    },
    async updateStatus() {
      try {
        const token = localStorage.getItem('access_token');

        const url = `${process.env.VUE_APP_GATEWAY_URL}/documents-api/${this.task.id}`
        const requestData = {
          file_id: this.task.file_id || null,
          subject: this.task.subject || '',
          description: this.task.description || '',
          status: this.selectedStatus || '',
          priority: this.task.priority || '',
          author_id: this.task.author_id || '',
          responsible_employee_id: this.assignedToUser.id || '',
          registration_date: this.task.registration_date || new Date().toISOString()
        };

        const response = await axios.put(url, requestData, {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (response.status === 200) {
          this.$emit('status-updated', this.task.id, this.selectedStatus);
          this.$notify({ group: 'foo', type: 'success', text: 'Статус обновлен' });
        } else {
          this.$notify({ group: 'foo', type: 'error', text: 'Не удалось обновить статус' });
        }
      } catch (error) {
        this.$notify({ group: 'foo', type: 'error', text: 'Не удалось обновить статус' });
      }
    }
  },
  computed: {
    statusClass() {
      if (this.selectedStatus === 'В обработке') return 'status-in-progress';
      if (this.selectedStatus === 'Завершено') return 'status-completed';
      if (this.selectedStatus === 'Отменено') return 'status-rejected';
      return '';
    },
    priorityIcon() {
      switch (this.task.priority) {
        case 'Низкий':
          return { icon: 'mdi-arrow-down', color: 'green' };
        case 'Средний':
          return { icon: 'mdi-scale-balance', color: 'blue' };
        case 'Важный':
          return { icon: 'mdi-alert', color: 'orange' };
        case 'Очень важный':
          return { icon: 'mdi-alert-circle', color: 'red' };
        case 'Бомба':
          return { icon: 'mdi-bomb', color: 'purple' };
        default:
          return { icon: 'mdi-help-circle', color: 'grey' };
      }
    }
  }

};
</script>

<style scoped>
.task-card {
  font-size: 14px;
}

.title-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.status-in-progress {
  color: blue;
}

.status-completed {
  color: green;
}

.status-rejected {
  color: red;
}
</style>
