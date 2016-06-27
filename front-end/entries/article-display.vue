<script>
	import Vue from 'vue';
  	import navbar from  '../components/navbar.vue';
  	import articleDetail from '../components/article-detail.vue'
  
  	var a = new Vue({
    	el: 'body',
    	components: { navbar,articleDetail }
  	})
</script>