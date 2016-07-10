<template>
    <div class="container-fluid main">
        <div class="col-xs-12 col-md-8">
            <section>
                <vs-card>
                    <div class="card-block article-main">
                        <h1 class="card-title">{{ topic.title }}</h1>
                        {{{ topic.content }}}

                        <p class="card-text text-muted hidden-sm-down">
                            <small>
                                {{ topic.asker.nickname }} 发表于 {{ topic.created_time | timesince }}
                            </small>
                        </p>
                    </div>
                    <vs-list-group flush class="hidden-md-up">
                        <vs-list-group-item>
                            发布于 {{ topic.created_time | timesince }}
                        </vs-list-group-item>
                        <vs-list-group-item>
                            更新于 {{ topic.updated_time | timesince }}
                        </vs-list-group-item>
                    </vs-list-group>
                </vs-card>
            </section>
            <hr>
            <vs-card v-for="reply in page.results">
                <div class="card-block article-main">
                    {{{ reply.content }}}

                    <p class="card-text text-muted">
                        <small>
                            {{ reply.author.nickname }} 发表于 {{ reply.created_time | timesince }}
                        </small>
                    </p>
                </div>
            </vs-card>
            <pager
                v-if="topicId"
                :url="`/api/topics/${topicId}/replies/`"
                :model.sync="page">
            </pager>
        </div>
        <div class="col-md-4 hidden-sm-down">
            <vs-card>
                <vs-list-group flush>
                    <vs-list-group-item>
                        发布于 {{ topic.created_time | timesince }}
                    </vs-list-group-item>
                    <vs-list-group-item>
                        更新于 {{ topic.updated_time | timesince }}
                    </vs-list-group-item>
                </vs-list-group>
            </vs-card>
        </div>
        <div class="col-xs-12 lg-no-padding">
            <editor
                :model.sync="reply"
                name="topic-reply-edit"
                :base-url="`/api/topics/${topicId}/replies/`"
                @submitted="editorSubmitted">
            </editor>
        </div>
    </div>
</template>

<style scoped>
    .main {
        word-wrap: break-word;
    }
</style>

<script>
    import Editor from 'misc/edit/Editor.vue'
    import DetailMixin from 'mixins/DetailMixin.es'
    import Pager from 'misc/Pager.vue'

    export default {
        mixins: [DetailMixin],
        components: {Editor, Pager},
        detailConfig: {
            baseURL: '/api/topics/',
            objectFieldName: 'topic',
            idFieldName: 'topicId'
        },
        data: () => ({
            topic: {},
            topicId: '',
            page: {},
            reply: {
                content: '',
                attachments: []
            }
        }),
        methods: {
            editorSubmitted (editor, reply) {
                this.page.results.push(reply)
            }
        }
    }
</script>