<template>
    <div class="container-fluid">
        <vs-card
            v-for="company in objects"
            class="col-xs-12 col-sm-6 col-md-4"
            >
            <div class="card-block">
                <h4 class="card-title text-center">{{ company.user_data.name }}</h4>
                <dl class="dl-horizontal">
                    <dt class="col-sm-3">板块</dt>
                    <dd class="col-sm-9">{{ company.user_data.sector }}</dd>
                    <dt class="col-sm-3">行业</dt>
                    <dd class="col-sm-9">{{ company.user_data.industry }}</dd>
                    <dt class="col-sm-3">介绍</dt>
                    <dd class="col-sm-9">{{ company.user_data.description }}</dd>
                </dl>
            </div>
        </vs-card>
        <infinite-loading 
            :on-infinite="load"
            class="col-xs-12">
        </infinite-loading>
    </div>
</template>

<script>
    import InfiniteLoadingMixin from 'components/mixins/InfiniteLoadingMixin.es'
    import InfiniteLoading from 'vue-infinite-loading'
    import { accounts } from 'consts.json'

    export default {
        mixins: [InfiniteLoadingMixin],
        components: { InfiniteLoading },
        data: () => ({
            objects: [],
            nextURL: ''
        }),
        computed: {
            baseURL () {
                return `/api/users/`
            },
            params () {
                return {
                    user_type: accounts.UserType.company
                }
            }
        },
        ready () {
            this.reset()
        }
    }
</script>