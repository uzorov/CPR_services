<template>
  <v-container class="d-flex justify-center align-center fill-height">
    <v-card class="pa-5" outlined rounded>
      <v-form ref="loginForm" v-model="valid" @submit.prevent="login">
        <v-text-field
          v-model="username"
          label="Логин"
          :rules="[rules.required]"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Пароль"
          type="password"
          :rules="[rules.required]"
          required
        ></v-text-field>
        <v-btn :disabled="!valid" @click="login" :loading="loading" class="mt-4">
          Войти
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      username: '',
      password: '',
      loading: false,
      rules: {
        required: value => !!value || 'Обязательное поле'
      }
    };
  },
  methods: {
    async login() {
      this.loading = true;
      try {
        const response = await fetch('https://www.uzorovkirill.ru/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });
        const data = await response.json();

        console.log("data", data);

        if (response.ok) {
          const token = data.access_token;
          localStorage.setItem('access_token', token);
          this.$emit('login-success', token);
          this.$notify({ group: 'foo', type: 'success', text: 'Авторизация успешна!' });
        } else {
          this.$notify({ group: 'foo', type: 'error', text: 'Ошибка авторизации!' });
        }
      } catch (error) {
        this.$notify({ group: 'foo', type: 'error', text: 'Ошибка сети!' });
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.v-container {
  min-height: 100vh;
}
.v-card {
  max-width: 400px;
  width: 100%;
  border-radius: 8px;
}
</style>
