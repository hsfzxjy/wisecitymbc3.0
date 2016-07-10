<template>
    <a v-link="link" @click="clicked">
        <i v-if="icon" class="fa fa-{{icon}}"></i> {{title}}
    </a>
</template>

<style scoped>
    a {
        display: block;
    }
</style>

<script>
    export default {
        props: {
            title: {
                type: String,
                required: true
            },
            icon: {
                type: String,
                default: ''
            },
            link: {
                type: String,
                required: true
            }
        },
        methods: {
            clicked () {
                this.$dispatch('BlockA:click', this)
            }
        }
    }
</script>