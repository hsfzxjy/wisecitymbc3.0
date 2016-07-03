<template>
    <div>
        <vs-card>
            <div class="card-header">
                <span class="label" style="background-color:#209E85">
                    @{{ article.author.nickname }}
                </span>
                <span class="label label-danger" v-if="article.is_top">
                    置顶
                </span>
            </div>
            <div class="card-block">
                <h1 class="card-title" style="text-align:center">{{ article.title }}</h1>
                <p class="card-text">
                    <template v-if="expanded">
                        {{{ article.content }}}
                    </template>
                    <template v-else>
                        {{ article.summary }}                        
                    </template>
                </p>
                <a 
                    class="btn btn-link pull-right" 
                    @click.stop="expanded = true" 
                    v-show="!expanded">
                    查看
                </a>
            </div>
            <div class="card-footer text-muted">
                {{ article.created_time }}
            </div>
        </vs-card>        
    </div>
</template>

<script>
    export default {
        props: {
            article: {
                type: Object,
                required: true
            },
            expanded: false
        }
    }
</script>