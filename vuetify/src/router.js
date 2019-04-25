import Cookies from 'js-cookie'

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
        if (savedPosition) return savedPosition
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
        },
        {
            path: "/about",
            name: "about",
            component: () => import( /* webpackChunkName: "about" */ "./views/About.vue")
        },
        {
            path: "/about/terms-of-service",
            name: "terms-of-service",
            component: () => import( /* webpackChunkName: "about" */ "./views/TermsOfService.vue")
        },
        // ======= STRUCTURES =======
        {
            path: "/structures",
            name: "structure-list",
            component: () => import( /* webpackChunkName: "structure" */ "./views/structure/StructureList.vue")
        },
        {
            path: "/structures/create",
            name: "structure-create",
            component: () => import( /* webpackChunkName: "structure" */ "./views/structure/StructureCreate.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/structures/:slug/manage",
            name: "structure-manage",
            component: () => import( /* webpackChunkName: "structure" */ "./views/structure/StructureManage.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/structures/:slug",
            name: "structure-detail",
            component: () => import( /* webpackChunkName: "structure" */ "./views/structure/StructureDetail.vue")
        },
        // ======= PROJECTS =======
        {
            path: "/projects",
            name: "project-list",
            component: () => import( /* webpackChunkName: "project" */ "./views/project/ProjectList.vue")
        },
        {
            path: "/projects/areas/:area",
            name: "project-list-byarea",
            component: () => import( /* webpackChunkName: "project" */ "./views/project/ProjectList.vue")
        },
        {
            path: "/projects/create",
            name: "project-create",
            component: () => import( /* webpackChunkName: "project" */ "./views/project/ProjectCreate.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/projects/:slug/manage",
            name: "project-manage",
            component: () => import( /* webpackChunkName: "project" */ "./views/project/ProjectManage.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/projects/:slug",
            name: "project-detail",
            component: () => import( /* webpackChunkName: "project" */ "./views/project/ProjectDetail.vue")
        },
        // ======= Evaluation =======
        {
            path: "/evaluation/:slug/entry",
            name: "evaluation-entry",
            component: () => import( /* webpackChunkName: "evaluation" */ "./views/evaluation/EvaluationEntry.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/projects/:slug/evaluation",
            name: "evaluation-detail",
            component: () => import( /* webpackChunkName: "evaluation" */ "./views/evaluation/EvaluationDetail.vue"),
            meta: {requiresAuth: true}
        },
        // ======= ACCOUNT =======
        {
            path: "/account/:slug?",
            name: "account",
            component: () => import( /* webpackChunkName: "account" */ "./views/account/Account.vue")
        },
        // ======= Catch-ALL Error =======
        {
            path: "*",
            name: "404",
            component: Error404,
        }
    ]
});


router.beforeEach((to, from, next) => {
    if(to.matched.some(record => record.meta.requiresAuth)) {
        // For a route marked as "requiresAuth", perform a check
        let hasAuth = Cookies.get("authorization") != null

        if (!hasAuth) {
            // Redirect to login
            console.log("force login for route")
            next({
                name: 'login',
                query: { redirect: to.fullPath }
            })
        } else {
            next()
        }

    }

    next()

})


export default router;