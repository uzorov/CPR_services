<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>
        <v-avatar>
          <img src="https://nvpsy.ru/img/index/6.png" alt="Logo" />
        </v-avatar>
        Цифровой помощник руководителя
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <UserMenu v-if="isLoggedIn" :user="user" @logout="handleLogout" />
    </v-app-bar>
    <v-main>
      <TaskList v-if="isLoggedIn" />
      <LoginForm v-else @login-success="handleLoginSuccess" />
      <notifications group="foo" position="top right" />
    </v-main>
  </v-app>
</template>

<script>
import UserMenu from './components/UserMenu.vue';
import TaskList from './components/TaskList.vue';
import LoginForm from './components/LoginForm.vue';

export default {
  components: {
    UserMenu,
    TaskList,
    LoginForm
  },
  data() {
    return {
      isLoggedIn: false,
      user: null
    };
  },
  methods: {
    async handleLoginSuccess(token) {
      try {
        console.log("token>>", token);
        const response = await fetch('https://www.uzorovkirill.ru/auth/user', {
          headers: {
            Authorization: `Bearer ${token}`
          },
          mode: "cors"
        });
        const userData = await response.json();
        this.user = userData;
        localStorage.setItem('user_id', this.user.id);
        this.isLoggedIn = true;
      } catch (error) {
        this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при получении данных пользователя!' });
      }
    },
    async handleLogout() {
      const token = localStorage.getItem('access_token');
      try {
        await fetch('https://www.uzorovkirill.ru/auth/logout', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        localStorage.removeItem('access_token');
        this.user = null;
        this.isLoggedIn = false;
        this.$notify({ group: 'foo', type: 'success', text: 'Вы вышли из аккаунта!' });
      } catch (error) {
        this.$notify({ group: 'foo', type: 'error', text: 'Ошибка при выходе из аккаунта!' });
      }
    }
  }
};
</script>

<style>
/* Добавьте стили по необходимости */
</style>
