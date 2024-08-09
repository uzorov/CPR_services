<template>
  <v-container>
    <v-row class="mb-2" justify="end">
      <v-col cols="auto">
        <v-btn v-if="userRole === 'Руководитель'" color="primary" @click="openTaskForm(false, null)">
          Добавить поручение
        </v-btn>
      </v-col>
    </v-row>

    <!-- Фильтры и поиск -->
    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-select
          v-model="filterStatus"
          :items="statusOptions"
          label="Фильтр по статусу"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          v-model="filterPriority"
          :items="priorityOptions"
          label="Фильтр по приоритету"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="searchQuery"
          label="Поиск по заголовку"
          clearable
          append-icon="mdi-magnify"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-expansion-panels>
      <!-- Поручения, назначенные на меня -->
      <v-expansion-panel>
        <v-expansion-panel-header>
          Поручения, назначенные на меня
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row v-if="users && users.length > 0">
            <v-col v-for="task in filteredAssignedTasks" :key="task.id" cols="12" md="4">
              <TaskCard :task="task" :users="users" @edit-task="openTaskForm(true, task)" @delete-task="deleteTask" />
            </v-col>
          </v-row>
          <v-row v-else>
            <v-col cols="12">
              <p>Загрузка...</p>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <!-- Поручения, созданные мной -->
      <v-expansion-panel>
        <v-expansion-panel-header>
          Поручения, созданные мной
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row v-if="users && users.length > 0">
            <v-col v-for="task in filteredCreatedTasks" :key="task.id" cols="12" md="4">
              <TaskCard :task="task" :users="users" @edit-task="openTaskForm(true, task)" @delete-task="deleteTask" />
            </v-col>
          </v-row>
          <v-row v-else>
            <v-col cols="12">
              <p>Загрузка...</p>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <TaskForm :isDialogOpen="isTaskFormOpen" :isEditMode="isEditMode" :task="currentTask" @save-task="saveTask"
      @update:isDialogOpen="updateTaskFormOpen" />
  </v-container>
</template>

<script>
import TaskCard from './TaskCard.vue';
import TaskForm from './TaskForm.vue';
import axios from 'axios';

export default {
  components: { TaskCard, TaskForm },
  data() {
    return {
      userRole: 'Специалист',
      assignedTasks: [],
      createdTasks: [],
      isTaskFormOpen: false,
      isEditMode: false,
      currentTask: null,
      currentUser: null,
      users: [],
      searchQuery: '',
      filterStatus: null,
      filterPriority: null,
      statusOptions: ['В обработке', 'Завершено', 'Отменено'],
      priorityOptions:  ['Низкий', 'Важный', 'Очень важный', 'Бомба'],
    };
  },
  created() {
    this.fetchUsers();
    this.fetchUserData();
    this.fetchTasks();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('https://www.uzorovkirill.ru/auth/users', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.users = response.data;
        console.log("users>>>", this.users);
      } catch (error) {
        console.error('Ошибка при загрузке списка пользователей:', error);
      }
    },

    async fetchUserData() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('https://www.uzorovkirill.ru/auth/user', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const userData = await response.json();
        this.currentUser = userData;
        this.userRole = userData.localized_role;
      } catch (error) {
        this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при получении данных пользователя!' });
      }
    },

    async fetchTasks() {
      try {
        const userId = localStorage.getItem('user_id');
        const token = localStorage.getItem('access_token');

        const assignedResponse = await axios.get(`https://www.uzorovkirill.ru/documents-api/assigned-tasks/${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const createdResponse = await axios.get(`https://www.uzorovkirill.ru/documents-api/created-tasks/${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.assignedTasks = assignedResponse.status === 200 && Array.isArray(assignedResponse.data) ? assignedResponse.data : [];
        this.createdTasks = createdResponse.status === 200 && Array.isArray(createdResponse.data) ? createdResponse.data : [];
        this.$notify({ group: 'foo', type: 'info', text: 'Поручения успешно загружены' });
        console.log('Assigned tasks:', this.assignedTasks);
        console.log('Created tasks:', this.createdTasks);
      } catch (error) {
        if (error.response && error.response.status === 404) {
          console.warn('Задачи не найдены, установка пустых массивов.');
          this.assignedTasks = [];
          this.createdTasks = [];
        } else {
          console.error('Ошибка при загрузке поручений:', error);
          this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при загрузке поручений!' });
        }
      }
    },

    openTaskForm(isEditMode, task) {
      this.isEditMode = isEditMode;
      this.currentTask = task;
      this.isTaskFormOpen = true;
    },

    updateTaskFormOpen(isOpen) {
      this.isTaskFormOpen = isOpen;
    },

    saveTask(taskData) {
      if (this.isEditMode) {
        const index = this.createdTasks.findIndex(task => task.id === this.currentTask.id);
        if (index !== -1) {
          this.$set(this.createdTasks, index, { ...this.currentTask, ...taskData });
        }
      } else {
        const newTask = { ...taskData, id: this.createdTasks.length + 1 };
        this.createdTasks.push(newTask);
      }
      //Обновляем список данных
      this.fetchTasks();
    },

    async deleteTask(task) {
      const token = localStorage.getItem('access_token');
      try {
        await axios.delete(`https://www.uzorovkirill.ru/documents-api/${task.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.createdTasks = this.createdTasks.filter(t => t.id !== task.id);
        this.$notify({ group: 'foo', type: 'success', text: 'Поручение удалено' });
      } catch (error) {
        console.error('Ошибка при удалении задачи:', error);
        this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при удалении задачи!' });
      }
    }
  },
  computed: {
    filteredAssignedTasks() {
      return this.assignedTasks.filter(task => {
        return (!this.filterStatus || task.status === this.filterStatus) &&
               (!this.filterPriority || task.priority === this.filterPriority) &&
               (!this.searchQuery || task.subject.toLowerCase().includes(this.searchQuery.toLowerCase()));
      });
    },
    filteredCreatedTasks() {
      return this.createdTasks.filter(task => {
        return (!this.filterStatus || task.status === this.filterStatus) &&
               (!this.filterPriority || task.priority === this.filterPriority) &&
               (!this.searchQuery || task.subject.toLowerCase().includes(this.searchQuery.toLowerCase()));
      });
    }
  }
}
</script>

<style scoped>
.v-btn {
  margin-bottom: 16px;
}

.task-card {
  font-size: 14px;
  line-height: 1.5;
  overflow: hidden;
}

.v-expansion-panel-content {
  padding: 10px;
}

.v-text-field {
  max-width: 400px;
}
</style>
