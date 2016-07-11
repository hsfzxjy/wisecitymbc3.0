<template>
    <div class="container-fluid card-columns">
            <vs-card v-for="company in companies">
                <div class="card-block">
                    <h4 class="card-title text-center">
                        <a v-link="`/users/${company.id}/`">
                            {{ company.user_data.name || '(空)' }}
                        </a>
                    </h4>
                    <dl class="dl-horizontal">
                        <dt class="col-sm-3">板块</dt>
                        <dd class="col-sm-9">{{ company.user_data.sector || '(空)' }} </dd>
                        <dt class="col-sm-3">行业</dt>
                        <dd class="col-sm-9">{{ company.user_data.industry || '(空)' }} </dd>
                        <dt class="col-sm-3">介绍</dt>
                        <dd class="col-sm-9">{{ company.user_data.description || '(空)' }} </dd>
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
    import InfiniteLoadingMixin from 'mixins/InfiniteLoadingMixin.es'
    import InfiniteLoading from 'vue-infinite-loading'
    import { accounts } from 'consts.es'

    export default {
        mixins: [InfiniteLoadingMixin],
        listConfig: {
            listFieldName: 'companies'
        },
        components: { InfiniteLoading },
        data: () => ({
            companies: [],
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