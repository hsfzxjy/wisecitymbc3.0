<template>

</template>
<script>
  import Vue from 'vue';
  import navbar from  '../components/navbar.vue';
  import lgform from '../components/lgform.vue';
  import articlesList from '../components/articles-list.vue'
  
  var index = new Vue({
    el: 'body',
    components: { navbar,lgform,articlesList }
  })
  console.log(index)
</script>
