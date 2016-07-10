<template>
    <vs-card>
        <div class="card-block">
            <a v-link="model.url">
                <h1 class="card-title text-xs-center">
                    {{ model.title }}
                </h1>
            </a>
        </div>
        <div class="card-block">
            {{{ model.content }}}
        </div>
        <div class="card-block text-muted">
            <p class="card-text">
                更新于 {{ model.updated_time | timesince }}
            </p>
            <p class="card-text">
                {{ model.author.nickname }} 发布于 {{ model.created_time | timesince }}
            </p>
        </div>
    </vs-card>
</template>

<script>
    export default {
        props: {
            model: {
                type: Object,
                required: true,
                twoWay: true
            }
        }
    }
</script>