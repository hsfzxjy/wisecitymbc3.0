<template>
    <div>
        <vs-jumbotron class="rows" v-if="!$loadingRouteData">
            <div 
                :class="['col-md-' + (hasUserData ? 4 : 12),'col-sm-12', 'text-center']"
                :style="{ 'border-right': (hasUserData ? '1px solid' : 0)}">
                <h1 class="jumbotron-heading">{{ user.nickname }}</h1>
                <p class="lead text-muted">@{{ user.username }}</p>
                <p class="lead text-muted">{{ userTypeName }}</p>
            </div>
            <hr class="m-y-2 hidden-md-up">
            <div 
                :class="['col-md-8','col-sm-12', 'text-center']"
                v-if="hasUserData">
                <dl class="dl-horizontal">
                    <dt class="col-sm-3">名称</dt>
                    <dd class="col-sm-9">{{ user.user_data.name }}</dd>
                    <dt class="col-sm-3">板块</dt>
                    <dd class="col-sm-9">{{ user.user_data.sector }}</dd>
                    <dt class="col-sm-3">行业</dt>
                    <dd class="col-sm-9">{{ user.user_data.industry }}</dd>
                    <dt class="col-sm-3">介绍</dt>
                    <dd class="col-sm-9">{{ user.user_data.description }}</dd>
                </dl>
            </div>
        </vs-jumbotron>
        <div class="rows" v-if="!$loadingRouteData">
            <div class="col-sm-12 col-md-3">
                <vs-card>
                    <div class="card-block">
                        <h4 style="margin-bottom: 0;">报告</h4>
                        <uploader
                            :files="reports"
                            :file-add-url="`/api/users/${id}/reports/`"
                            browse-button-id="reports-uploader">
                            <span id="reports-uploader">upload</span>
                        </uploader>
                    </div>
                    <report-list :user-id="id" :reports.sync="reports"></report-list>
                </vs-card>
            </div>
            <div class="col-sm-12 col-md-9">
                <article-list
                    :other-params="{ author__id: id }">
                </article-list>
            </div>
        </div>
    </div>
</template>

<script>
    import _ from 'lodash'
    import Uploader from 'components/Uploader.vue'
    import ReportList from 'components/lists/ReportList.vue'
    import ArticleList from 'components/lists/ArticleList.vue'
    import { StrUtils } from 'utils/index.es'
    import { USER_TYPES } from 'components/consts.es'
 
    export default {
        components: { ReportList, ArticleList, Uploader },
        data: () => ({
            user: null,
            id: '',
            reports: []
        }),
        computed: {
            hasUserData () {
                return !_.isNull(this.user.user_data)
            },
            userTypeName () {
                return USER_TYPES[this.user.user_type]
            }
        },
        route: {
            canActivate (transition) {
                let id = transition.to.params.id
                return id === undefined || StrUtils.isDigits(id)
            },
            data (transition) {
                let id = transition.to.params.id || 'me'
                
                return this.$http.get(`/api/users/${id}/`)
                    .then(res => {
                        this.user = res.data
                        this.id = res.data.id
                    })
            }
        },
        methods: {

        }
    }
</script>