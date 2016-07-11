<template>
    <div>
        <vs-jumbotron class="rows" v-if="!$loadingRouteData">
            <div 
                :class="['col-md-' + (hasUserData ? 4 : 12),'col-sm-12', 'text-xs-center']">
                <h1 class="jumbotron-heading">{{ user.nickname }}</h1>
                <p class="lead text-muted">@{{ user.username }}</p>
                <p class="lead text-muted">{{ userTypeName }}</p>
            </div>
            <hr class="m-y-2 hidden-md-up">
            <div 
                :class="['col-md-8','col-sm-12', 'text-center']"
                v-if="hasUserData">
                <editable 
                    :editable="user.user_data.perms.change"
                    :model.sync="user.user_data" 
                    :options="editableOptions"
                    :save-action="saveAction">
                    <dl class="dl-horizontal">
                        <dt class="col-sm-3">名称</dt>
                        <dd class="col-sm-9" edit="name">{{ user.user_data.name }}</dd>
                        <dt class="col-sm-3">板块</dt>
                        <dd class="col-sm-9" edit="sector">{{ user.user_data.sector }}</dd>
                        <dt class="col-sm-3">行业</dt>
                        <dd class="col-sm-9" edit="industry">{{ user.user_data.industry }}</dd>
                        <dt class="col-sm-3">介绍</dt>
                        <dd class="col-sm-9" edit="description">{{ user.user_data.description }}</dd>
                    </dl>
                </editable>
            </div>
        </vs-jumbotron>
        <div class="rows" v-if="!$loadingRouteData">
            <div class="col-sm-12 col-md-3 xs-no-padding" v-if="hasUserData">
                <vs-card>
                    <div class="card-block">
                        <h4>
                            报告
                            <vs-buttons 
                                id="reports-uploader"
                                variant="primary"
                                size="sm"
                                class="pull-xs-right clearfix"
                                :disabled="uploadStatus.uploading">
                                添加
                            </vs-buttons>
                        </h4>
                        <uploader
                            :files="reports"
                            :file-add-url="`/api/users/${id}/reports/`"
                            :upload-status.sync="uploadStatus"
                            browse-button-id="reports-uploader">
                        </uploader>
                        <vs-progress 
                            v-show="uploadStatus.uploading"
                            variant="success"
                            :value="uploadStatus.percent" 
                            style="margin-bottom: 0;"
                            striped>
                        </vs-progress>
                    </div>
                    <report-list :user-id="id" :reports.sync="reports"></report-list>
                </vs-card>
            </div>
            <div class="col-sm-12 col-md-{{ hasUserData ? 9 : 12}} xs-no-padding">
                <article-list
                    :other-params="{ author__id: id }">
                </article-list>
            </div>
        </div>
    </div>
</template>

<script>
    import Uploader from 'misc/Uploader.vue'
    import ReportList from './ReportList.vue'
    import ArticleList from 'articles/ArticleList.vue'
    import { StrUtils } from 'utils/index.es'
    import { USER_TYPES } from 'consts.es'
 
    export default {
        components: { ReportList, ArticleList, Uploader },
        data: () => ({
            user: null,
            id: '',
            reports: [],
            uploadStatus: {
                uploading: false,
                percent: 0
            },
            editableOptions: {
                description: {
                    type: 'textarea'
                }
            }
        }),
        computed: {
            hasUserData () {
                return !!(this.user.user_data)
            },
            userTypeName () {
                return USER_TYPES[this.user.user_type]
            },
            saveAction () {
                return {
                    method: 'patch',
                    url: `/api/users/${this.id}/userdata/`,
                    dropArray: true
                }
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
        events: {
            logout () {
                this.user = null

                return true
            }
        }
    }
</script>