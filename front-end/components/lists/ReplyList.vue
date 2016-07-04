<template>
    <div v-for="reply in replies">
        {{reply.content}}
    </div>
</template>

<script>
    export default {
        props: {
            topicId: {
                type: String,
                required: true
            },
            replies: {
                type: Array,
                required: true,
                twoWay: true
            }
        },
        ready () {
            this.$http
                .get(`/api/topics/${this.topicId}/replies/`, {
                    params: { limit: -1 }
                })
                .then(res => {
                    this.replies = res.data.results
                })
        }
    }
</script>