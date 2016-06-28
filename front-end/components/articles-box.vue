<template>
	<ul class="nav nav-pills">
		<li class="nav-item"><a class="nav-link">Home</a></li>
  		<li class="nav-item"><a class="nav-link">Profile</a></li>
  		<li class="nav-item"><a class="nav-link">Messages</a></li>
	</ul>
	<div class="col-sm-3 no-padding" id="article-title" style="padding-left:0px;">
		<div class="list-group">
			<a v-for="item in articles" @click="loadArticle($index)" id="article-{{$index}}" class="list-group-item"><b>{{item.title}}</b><br>{{item.summary}}</a>
		</div>
	</div>
	<div class="col-sm-9 no-padding">
		<div class="article-header">
			作者:{{articles[aid].author.username}}<br>
			时间:{{articles[aid].created_time}}<br>
			<h3>{{articles[aid].title}}</h3>
		</div>
		<div class="article-content">
			{{articles[aid].content}}{{articleType}}
		</div>
		<div class="article-footer">
			
		</div>
	</div>
</template>

<script>
	export default {
		props: [''],
		data() {
			return {
				articles: [],
				aid:0,
				articleType:0,
			}
		},
		ready() {
			var self = this;
			var promise=$.ajax({
				url:'/api/articles',
				type: 'GET',
				success(data) {
					self.$data.articles = data.results
					console.log(self.$data.articles);
					console.log('1')
					console.log(a_s)
				}
			})
		},
		methods: {
			loadArticle(index){
				$(".list-group .list-active").removeClass('list-active')
				$('#article-'+index).addClass('list-active')
				this.aid = index
			}
		}
	}
</script>