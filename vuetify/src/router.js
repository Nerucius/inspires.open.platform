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
    scrollBehavior (to, from, savedPosition) {
        // Scroll to top on any route changes
        return { x: 0, y: 0 }
    },
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
        // ======= PROJECTS =======
        {
            path: "/projects",
            name: "project-list",
            component: () => import( /* webpackChunkName: "project-list" */ "./views/project/List.vue")
        },
        {
            path: "/projects/create",
            name: "project-create",
            component: () => import( /* webpackChunkName: "project-create" */ "./views/project/Create.vue")
        },
        {
            path: "/projects/:slug/manage",
            name: "project-manage",
            component: () => import( /* webpackChunkName: "project-manage" */ "./views/project/Manage.vue")
        },
        {
            path: "/projects/:slug",
            name: "project-detail",
            component: () => import( /* webpackChunkName: "project-detail" */ "./views/project/Detail.vue")
        },
        // ======= ACCOUNT =======
        {
            path: "/account",
            name: "account",
            component: () => import( /* webpackChunkName: "account-projects" */ "./views/account/Account.vue")
        },
        {
            path: "/account/projects",
            name: "account-projects",
            component: () => import( /* webpackChunkName: "account-projects" */ "./views/account/MyProjects.vue")
        },
        {
            path: "*",
            name: "404",
            component: Error404,
        }
    ]
});

export default router;