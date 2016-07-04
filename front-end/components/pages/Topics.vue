<template>
    <div class="container-fluid">
        <div class="col-md-3 col-sm-12">
            <a 
                class="btn btn-success"
                v-link="/topicEdit/"
            >发帖</a>
        </div>
        <div class="col-md-9 col-sm-12">
            <vs-card 
                v-for="topic in objects">
                <div class="card-block">
                    <h3 class="card-title">
                        {{ topic.title }}
                    </h3>
                </div>
            </vs-card>
            <infinite-loading
                :on-infinite="load">
            </infinite-loading>
        </div>
    </div>
</template>

<script>
    import InfiniteLoadingMixin from 'components/mixins/InfiniteLoadingMixin.es'

    export default {
        mixins: [InfiniteLoadingMixin],
        data: () => ({
            objects: [],
            nextURL: '',
            baseURL: `/api/topics/`,
            params: {}
        }),
        ready () {
            this.reset()
        }
    }
</script>