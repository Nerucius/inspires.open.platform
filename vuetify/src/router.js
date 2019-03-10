import Vue from "vue";
import Router from "vue-router";
import Meta from 'vue-meta'

import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import Error404 from "./views/error/404.vue";

Vue.use(Router);
Vue.use(Meta);

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: "/login",
            name: "login",
            component: Login,
        },
        {
            path: "/register",
            name: "register",
            component: () => import( /* webpackChunkName: "register" */ "./views/Register.vue"),
        },
        {
            path: "/",
            name: "home",
            component: Home,
            // TODO: Add Vue-meta plugin
            meta : { title: "Homepage - Campus Virtual "}
        },
        {
            path: "/about",
            name: "about",
            component: () => import( /* webpackChunkName: "about" */ "./views/About.vue")
        },
        {
            path: "*",
            name: "404",
            component: Error404,
        }
    ]
});

export default router;