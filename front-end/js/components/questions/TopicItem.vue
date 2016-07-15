<template>
    <vs-card>
        <div class="card-block">
            <div class="btn-group operation pull-xs-right">
                <button class="btn btn-default dropdown-toggle btn-sm" data-toggle="dropdown">
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu dropdown-menu-right">
                    <li v-if="model.perms.change">
                        <a 
                            class="dropdown-item" 
                            v-link="'/edit/topics/'+model.id+'/'">
                            编辑
                        </a>
                    </li>
                    <li v-if="model.perms.delete">
                        <delete-button
                            :list.sync="list"
                            :index="index"
                            :id="model.id"
                            base-url="/api/topics/">
                        <a class="dropdown-item" href="javascript:void 0">删除</a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="card-block">
            <a v-link="model.url">
                <h1 class="card-title text-xs-center">
                    {{ model.title }}
                </h1>
            </a>
        </div>
        <div class="card-block">
            {{{ model.content }}}
        </div>
        <div class="card-block text-muted">
            <p class="card-text">
                更新于 {{ model.updated_time | timesince }}
            </p>
            <p class="card-text">
                {{ model.asker.nickname }} 发布于 {{ model.created_time | timesince }}
            </p>
            <p class="card-text" v-if="model.replies_count">
                {{ model.replies_count }} 条回复
            </p>
        </div>
    </vs-card>
</template>

<script>
    import DeleteButton from 'misc/DeleteButton.vue'

    export default {
        components: { DeleteButton },
        props: {
            model: {
                type: Object,
                required: true,
                twoWay: true
            },
            list: {
                type: Array,
                required: true,
                twoWay: true
            },
            index: {
                type: Number,
                required: true
            }
        }
    }
</script>