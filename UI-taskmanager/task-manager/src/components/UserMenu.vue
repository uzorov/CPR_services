<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on">
        <div class="square-avatar">
          <img
            src="https://do.chel-meteor.ru/wp-content/uploads/2023/02/ab12618478634121072650b79952f9906de76c3cd450f49d27c4f101c41bf301.png?lm=1710867825"
            alt="User Avatar"
          />
        </div>
      </v-btn>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ user.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ user.localized_role }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item @click="logout">  
        <v-list-item-title>Выйти</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  props: {
    user: Object
  },
  methods: {
    logout() {
      this.$emit('logout');
    }
  }
};
</script>
<style scoped>

.square-avatar {
  width: 40px; 
  height: 40px; 
  border-radius: 4px; 
  overflow: hidden; 
}

.square-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover; 
}
</style>