// src/router/index.ts
import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../pages/qqEmail.vue"; // 引入页面组件

// 定义路由配置
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/liepin",
    name: "liepin",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../pages/liepin.vue"),
  },
];

// 创建路由器实例
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
