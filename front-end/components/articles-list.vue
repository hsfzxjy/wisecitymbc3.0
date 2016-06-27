<template>
	<ul class="list-group list-wmbc">
		<li class="list-group-item"><a href="#">Cras justo odio</a></li>
		<li class="list-group-item"><a href="#">Cras justo odio</a></li>
		<li class="list-group-item"><a href="#">Cras justo odio</a></li>
		<li class="list-group-item"><a href="#">Cras justo odio</a></li>
		<li class="list-group-item"><a href="#">Cras justo odio</a></li>
		<li class="list-group-item">MSG: {{ msg }}</li>
		<li class="list-group-item" v-for="item in articles"><a href="/api/articles/{{item.id}}">{{item.title}}</a></li>
	</ul>
</template>

<script>
	export default {
		data() {
			return {
				articles: []
			}
		},
		created() {
			var self = this;
			$.ajax({
				url:'/api/articles',
				type: 'GET',
				success(data) {
					self.$data.articles = data.results
					console.log(self.$data.articles);
				}
			})
		}
	}
</script>