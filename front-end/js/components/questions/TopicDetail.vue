<template>
    <div class="container-fluid main">
        <div class="col-xs-12 col-md-8 sm-no-padding">
            <section>
                <vs-card>
                    <div class="card-block article-main">
                        <h1 class="card-title text-xs-center">{{ topic.title }}</h1>
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
                        <vs-list-group-item v-if="topic.perms.change">
                            <vs-link
                                title="编辑"
                                :link="'/edit/topics/'+topic.id+'/'">
                            </vs-link>
                        </vs-list-group-item>
                    </vs-list-group>
                </vs-card>
            </section>
            <hr>
            <vs-card v-for="reply in replies">
                <div class="card-block article-main">
                    {{{ reply.content }}}

                    <p class="card-text text-muted">
                        <small>
                            {{ reply.author.nickname }} 发表于 {{ reply.created_time | timesince }}
                        </small>
                    </p>
                </div>
            </vs-card>
            <list
                v-if="topicId"
                :url="'/api/topics/'+topicId+'/replies/'"
                :model.sync="replies"
                type="pager">
            </list>
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
                    <vs-list-group-item v-if="topic.perms.change">
                        <vs-link
                            title="编辑"
                            :link="'/edit/topics/'+topic.id+'/'">
                        </vs-link>
                    </vs-list-group-item>
                </vs-list-group>
            </vs-card>
        </div>
        <div class="col-xs-12 lg-no-padding">
            <editor
                v-if="!$loadingRouteData"
                :model.sync="reply"
                name="topic-reply-edit"
                :base-url="'/api/topics/'+topicId+'/replies/'"
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
    import DetailMixin from 'mixins/DetailMixin'

    export default {
        mixins: [DetailMixin],
        components: {Editor},
        detailConfig: {
            baseURL: '/api/topics/',
            objectFieldName: 'topic',
            idFieldName: 'topicId'
        },
        data: () => ({
            topic: {},
            topicId: '',
            replies: [],
            reply: {
                content: '',
                attachments: []
            }
        }),
        methods: {
            editorSubmitted (editor, reply) {
                this.replies.push(reply)
            }
        }
    }
</script>