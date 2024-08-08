<template>
  <v-dialog v-model="localDialogOpen" max-width="600px" persistent>
    <v-card>
      <v-card-title>
        <span v-if="isEditMode">Редактировать поручение</span>
        <span v-else>Создать поручение</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-text-field v-model="taskData.subject" label="Тема"
            :rules="[v => !!v || 'Тема обязательна']"></v-text-field>
          <v-textarea v-model="taskData.description" label="Текст документа" auto-grow :rows="10"
            :rules="[v => !!v || 'Описание обязательно']"></v-textarea>
          <v-row class="d-flex justify-end">
            <v-progress-linear v-if="isRecording" indeterminate color="primary" class="mt-2"></v-progress-linear>

            <v-dialog v-model="isUploading" persistent max-width="290">
              <v-card>
                <v-card-text class="text-center">
                  <v-progress-circular indeterminate size="68" width="4" color="primary"></v-progress-circular>
                  <div>Расшифровка голосового сообщения...</div>
                </v-card-text>
              </v-card>
            </v-dialog>


            <v-btn icon @click="startVoiceRecording">
              <v-icon>mdi-microphone</v-icon>
            </v-btn>
            <v-btn icon @click="fixTextErrors">
              <v-icon>mdi-text-box-edit-outline</v-icon>

            </v-btn>
          </v-row>
          <v-select v-model="taskData.status" :items="statuses" label="Статус"
            :rules="[v => !!v || 'Статус обязателен']"></v-select>
          <v-select v-model="taskData.priority" :items="priorities" label="Приоритет"></v-select>
          <v-text-field v-model="taskData.registration_date" label="Дата создания"
            :rules="[v => !!v || 'Дата создания обязательна']" type="date"></v-text-field>

          <v-select v-model="taskData.assignedTo" :items="users" item-text="name" item-value="id" label="Назначить на"
            required></v-select>
          <!-- Другие поля формы -->
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="close">Отмена</v-btn>
        <v-btn color="blue darken-1" text @click="save">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios';
import RecordRTC from 'recordrtc';

export default {
  props: {
    isDialogOpen: Boolean,
    isEditMode: Boolean,
    task: Object
  },
  data() {
    return {
      localDialogOpen: this.isDialogOpen,
      taskData: this.task || {
        assignedTo: null,
        subject: '',
        description: '',
        status: '',
        priority: '',
        registrationDate: '',
        recorder: null,
        audioBlob: null
      },
      statuses: ['В обработке', 'Завершено', 'Отменено'],
      priorities: ['Низкий', 'Важный', 'Очень важный', 'Бомба'],
      users: [],
      valid: true,
      isRecording: false,
      isUploading: false
    };
  },
  watch: {
    isDialogOpen(newVal) {
      this.localDialogOpen = newVal;
      if (!newVal) {
        this.resetForm(); // Очистка формы при закрытии
      }
    },
    task(newTask) {
      this.taskData = newTask || {
        id: null,
        assignedTo: null,
        subject: '',
        description: '',
        status: '',
        priority: '',
        registration_date: ''
      };
      this.taskData.assignedTo = newTask.responsible_employee_id;
      const d = new Date(newTask.registration_date);
      this.taskData.registration_date = d.toISOString().split('T')[0];
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://87.242.86.68/auth/users', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.users = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке списка пользователей:', error);
      }
    },
    close() {
      this.localDialogOpen = false;
      this.$emit('update:isDialogOpen', false);
      this.resetForm();
    },
    async save() {
      const token = localStorage.getItem('access_token');
      if (this.$refs.form.validate()) {
        const url = this.isEditMode
          ? `http://87.242.86.68:83/documents-api/${this.taskData.id}/`
          : 'http://87.242.86.68:83/documents-api/';

        const userId = localStorage.getItem('user_id');
        const requestData = {
          file_id: this.taskData.file_id || null, // Можно заменить на пустую строку или другую логику для незаполненных полей
          subject: this.taskData.subject || '',
          description: this.taskData.description || '',
          status: this.taskData.status || '',
          priority: this.taskData.priority || '',
          author_id: userId || '',
          responsible_employee_id: this.taskData.assignedTo || '',
          registration_date: this.taskData.registration_date || new Date().toISOString()
        };

        console.log('Отправляемый объект:', requestData);
        console.log('Отправляемый объект по адресу:', url);

        try {
          if (this.isEditMode) {
            await axios.put(url, requestData, {
              headers: { Authorization: `Bearer ${token}` }
            });
          } else {
            await axios.post(url, requestData, {
              headers: { Authorization: `Bearer ${token}` }
            });
          }
          this.taskData.responsible_employee_id = this.taskData.assignedTo;
          this.$emit('save-task', this.taskData);
          this.$notify({ group: 'foo', type: 'info', text: 'Поручение обновлено' });
          this.close();
        } catch (error) {
          console.error('Ошибка при сохранении задачи:', error);
          this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при сохранении задачи!' });
        }
      }
    },
    async startVoiceRecording() {
      if (this.isRecording) {
        this.recorder.stopRecording(async () => {
          this.audioBlob = this.recorder.getBlob();
          console.log('Audio Blob создан:', this.audioBlob);

          this.isRecording = false; // Скрыть индикатор записи
          this.isUploading = true; // Показать индикатор загрузки

          const formData = new FormData();
          formData.append('file', this.audioBlob, 'audio.webm');

          try {
            this.$notify({ group: 'foo', type: 'info', text: 'Транскрибация аудио началась' });
            const response = await axios.post('http://87.242.86.68:84/transcribe-audio', formData, {
              headers: { 'Content-Type': 'multipart/form-data' }
            });

            const transcription = response.data.transcription;
            if (Array.isArray(transcription)) {
              this.taskData.description = transcription[0];
            } else {
              this.taskData.description = transcription;
            }


            if (Array.isArray(this.taskData.description)) {
              this.taskData.description = this.taskData.description[0];
            }
            if (this.taskData.description == '') {
              this.$notify({ group: 'foo', type: 'warning', text: 'Сервер перегружен... Повторите попытку' });
            }
            else {
              this.$notify({ group: 'foo', type: 'success', text: 'Текст успешно транскрибирован' });
            }
          } catch (error) {
            console.error('Ошибка при транскрибировании аудио:', error);
            this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при транскрибировании аудио' });
          } finally {
            this.isUploading = false; // Скрыть индикатор загрузки
          }
        });
      } else {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.recorder = new RecordRTC(stream, {
            type: 'audio',
            mimeType: 'audio/webm',
            recorderType: RecordRTC.MediaStreamRecorder,
            timeSlice: 1000,
            ondataavailable: (blob) => {
              console.log('Audio chunk received:', blob);
            },
          });

          this.recorder.startRecording();
          this.isRecording = true; // Показать индикатор записи
          console.log('Запись началась');
          this.$notify({ group: 'foo', type: 'info', text: 'Запись началась (Повторно нажмите для окончания)' });
        } catch (error) {
          console.error('Ошибка при доступе к микрофону:', error);
          this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при доступе к микрофону' });
        }
      }
    },
    async fixTextErrors() {
      try {
        const response = await axios.post('http://87.242.86.68:84/correct-text', {
          text: this.taskData.description
        });

        // Вставка исправленного текста в форму
        this.taskData.description = response.data.corrected_text[0];

        this.$notify({ group: 'foo', type: 'success', text: 'Текст успешно исправлен' });
      } catch (error) {
        console.error('Ошибка при исправлении текста:', error);
        this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при исправлении текста' });
      }
    },
    resetForm() {
      this.taskData = {
        assignedTo: null,
        subject: '',
        description: '',
        status: '',
        priority: '',
        registrationDate: ''
      };
    }
  }
}
</script>

<style scoped>
/* Стили для формы, если необходимо */
</style>
