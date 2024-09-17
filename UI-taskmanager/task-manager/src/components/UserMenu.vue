<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on, attrs }">
    
          <v-btn text rounded v-bind="attrs" v-on="on" class="pa-6">
        <!-- Разметка для надписи -->
          <div align="left">
            <span class="font-weight-bold dark-grey--text">{{ user.name }}</span>
            <br />
            <span class="text-caption grey--text">{{ user.localized_role }}</span>
          </div>
  
          <v-avatar size="40" class="ml-2">
            <v-icon x-large color="dark-grey">mdi-account-tie</v-icon>
          </v-avatar>
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