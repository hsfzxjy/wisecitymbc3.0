<template>
    <div class="container-fluid">
        <div class="col-md-3 col-sm-12">
            <a 
                class="btn btn-success btn-block"
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
                v-for="topic in page.results"
                :model.sync="topic">
            </topic-item>
            <pager
                url="/api/topics/"
                :model.sync="page">
            </pager>
        </div>
    </div>
</template>

<script>
    import Pager from 'misc/Pager.vue'
    import TopicItem from './TopicItem.vue'

    export default {
        components: { TopicItem, Pager },
        data: () => ({
            page: {},
            nextURL: '',
            baseURL: `/api/topics/`,
            params: {}
        })
    }
</script>