<template>
    <div class="container-fluid">
        <div class="col-md-3 col-sm-12">
            <a 
                class="btn btn-success btn-block"
                v-if="perms.questions.topic.add"
                v-link="'/edit/topics/'">
                发帖
            </a>
            <vs-buttons
                block
                variant="info"
                class="pull-xs-rigsht"
                @click="$broadcast('Pager:refresh')">
                刷新
            </vs-buttons>
        </div>
        <div class="col-md-9 col-sm-12">
            <topic-item
                v-for="topic in topics"
                :list.sync="topics"
                :index="$index"
                :model.sync="topic">
            </topic-item>
            <list
                url="/api/topics/"
                :model.sync="topics"
                type="pager">
            </list>
        </div>
    </div>
</template>

<script>
    import TopicItem from './TopicItem.vue'

    export default {
        components: { TopicItem },
        data: () => ({
            topics: [],
            nextURL: '',
            baseURL: `/api/topics/`,
            params: {}
        }),
        vuex: {
            getters: {
                perms: state => state.auth.perms
            }
        },
        ready () {
            this.$broadcast('List:reload')
        }
    }
</script>