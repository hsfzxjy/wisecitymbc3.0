<template>
    <div>
        <vs-card>
            <div class="card-block">
                <span class="tag label-1">
                    @{{ article.author.nickname }}
                </span>
                <span class="tag tag-danger" v-if="article.is_top">
                    置顶
                </span>
                <div class="btn-group operation pull-xs-right">
                    <button class="btn btn-default dropdown-toggle btn-sm" data-toggle="dropdown">
                        <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-right">
                        <li v-if="article.perms.change">
                            <a 
                                class="dropdown-item" 
                                v-link="'/edit/articles/'+article.id+'/'">
                                编辑
                            </a>
                        </li>
                        <li v-if="article.perms.delete">
                            <delete-button
                                :list.sync='list'
                                :index="index"
                                base-url="/api/articles/"
                                :id="article.id">
                                <a class="dropdown-item" href="javascript:void 0">删除</a>
                            </delete-button>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="card-block article-main">
                <h1 class="card-title" style="text-align:center">
                    <a v-link="article.url">{{ article.title }}</a>
                </h1>
                <div class="card-text">
                    <div v-if="expanded">
                        <div class="article-content">
                            {{{ article.content }}}
                        </div>
                    </div>
                    <p v-if="!expanded" @click="expanded = true">
                        {{ article.summary }}
                        <span style='color:rgba(155, 140, 103, 1);cursor:pointer'> |点击展开阅读</span>
                    </p>
                </div>
                <file-list
                    :model.sync="article.attachments">
                </file-list>
                <p class="card-text">
                    <small class="text-muted">
                        {{ article.created_time | timesince }}
                    </small>
                </p>
                <div class="card-text" v-if="article.tags.length">
                    <i class="fa fa-tags"></i>
                    <vs-badge
                        v-for="tag in article.tags"
                        variant="info">
                        {{tag}}
                    </vs-badge>
                </div>
            </div>
        </vs-card>        
    </div>
</template>

<style>
    .operation button {
        line-height: 1;
        background: transparent;
    }    
</style>

<script>
    import FileList from 'files/FileList.vue'
    import DeleteButton from 'misc/DeleteButton.vue'

    export default {
        components: { FileList, DeleteButton },
        props: {
            article: {
                type: Object,
                required: true
            },
            list: {
                type: Array,
                required: true,
                twoWay: true
            },
            index: {
                type: Number,
                required: true
            },
            expanded: false
        }
    }
</script>