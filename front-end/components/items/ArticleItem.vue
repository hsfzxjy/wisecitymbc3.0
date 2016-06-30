<template>
    <div>
        <vs-card>
            <div class="card-block">
                <h4 class="card-title">{{ article.title }}</h4>
                {{{ article.content }}}
            </div>
        </vs-card>        
    </div>
</template>

<script>
    export default {
        props: {
            article: {
                type: Object,
                required: true
            }
        }
    }
</script>