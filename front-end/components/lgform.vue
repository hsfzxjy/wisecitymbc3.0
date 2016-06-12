<template>
  <div class="container">
    <form id="login-form" style="margin-top:20px">
      <div class="form-group">
        <div class="input-group">
          <span class="input-group-addon"><i class="fa fa-user fa-fw" style="color:#333;"></i></span>
          <input type="text" class="form-control form-login" v-model="un" @focus="clearError" placeholder="请输入用户名" ><span class="input-group-addon "  v-show="iE""><i class="fa fa-exclamation-circle" style="color:#920;"></i></span>
        </div>
      </div>
      <div class="form-group">
        <div class="input-group">
          <div class="input-group-addon"><i class="fa fa-key fa-fw" style="color:#333;"></i></div>
          <input type="password" class="form-control form-login" v-model="pw" @focus="clearError" placeholder="请输入密码" ><span class="input-group-addon" v-show="iE"><i class="fa fa-exclamation-circle" style="color:#920;"></i></span>
        </div>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-login" @click.prevent="validate">登录</button>
      </div>
    </form>
  </div>
</template>
<script>

export default {
  data() {
    return {
      iE: false,
      un:'',
      pw:''
    }
  },
  methods: {
    validate() {
      this.iE = ((!this.un)||(!this.pw))
    },
    clearError() {
      this.iE=false
    }
  }
}
</script>