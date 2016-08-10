<template>
    <div>
        <div class="container-fluid card-columns">
            <vs-card v-for="company in companies">
                <div class="card-block">
                    <h4 class="card-title text-center">
                        <a v-link="'/users/'+company.id+'/'">
                            {{ company.username }} 
                            {{ company.user_data.name || '(无昵称)' }}
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
        </div>
        <list
            url="/api/users/"
            :model.sync="companies"
            :params="params">
        </list>
    </div>
</template>

<script>
    export default {
        data: () => ({
            companies: []
        }),
        computed: {
            params () {
                return {
                    user_type: consts.UserType.company
                }
            }
        },
        ready () {
            this.$broadcast('List:reload')
        }
    }
</script>