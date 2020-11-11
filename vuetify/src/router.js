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
            path: "/reset-password",
            name: "reset-password",
            component: () => import( /* webpackChunkName: "reset-password" */ "./views/account/ResetPassword.vue"),
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
            path: "/about-us",
            name: "about",
            component: () => import( /* webpackChunkName: "about" */ "./views/About.vue")
        },
        {
            path: "/about-us/terms-of-service",
            name: "terms-of-service",
            component: () => import( /* webpackChunkName: "terms-of-service" */ "./views/about/TermsOfService.vue")
        },
        {
            path: "/about-us/legal-notice",
            name: "legal-notice",
            component: () => import( /* webpackChunkName: "legal-notice" */ "./views/about/LegalNotice.vue")
        },
        {
            path: "/about-us/privacy-policy",
            name: "privacy-policy",
            component: () => import( /* webpackChunkName: "privacy-policy" */ "./views/about/PrivacyPolicy.vue")
        },
        {
            path: "/about-us/cookie-policy",
            name: "cookie-policy",
            component: () => import( /* webpackChunkName: "cookie-policy" */ "./views/about/CookiePolicy.vue")
        },
        // ======= SEARCH =======
        {
            path: "/search",
            name: "search",
            component: () => import( /* webpackChunkName: "search" */ "./views/Search.vue")
        },
        // ======= STRUCTURES =======
        {
            path: "/structures",
            name: "structure-list",
            component: () => import( /* webpackChunkName: "structure-list" */ "./views/structure/StructureList.vue")
        },
        {
            path: "/structures/create",
            name: "structure-create",
            component: () => import( /* webpackChunkName: "structure-create" */ "./views/structure/StructureCreate.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/structures/:slug/manage",
            name: "structure-manage",
            component: () => import( /* webpackChunkName: "structure-manage" */ "./views/structure/StructureManage.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/structures/:slug",
            name: "structure-detail",
            component: () => import( /* webpackChunkName: "structure-detail" */ "./views/structure/StructureDetail.vue")
        },
        // ======= PROJECTS =======
        {
            path: "/projects",
            name: "project-list",
            component: () => import( /* webpackChunkName: "project-list" */ "./views/project/ProjectList.vue")
        },
        {
            path: "/projects/areas/:area",
            name: "project-list-byarea",
            component: () => import( /* webpackChunkName: "project-list" */ "./views/project/ProjectList.vue")
        },
        {
            path: "/projects/create",
            name: "project-create",
            component: () => import( /* webpackChunkName: "project-create" */ "./views/project/ProjectCreate.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/projects/:slug/manage",
            name: "project-manage",
            component: () => import( /* webpackChunkName: "project-manage" */ "./views/project/ProjectManage.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/projects/:slug",
            name: "project-detail",
            component: () => import( /* webpackChunkName: "project-detail" */ "./views/project/ProjectDetail.vue")
        },
        // ======= Evaluation =======
        {
            path: "/help-center/:page?",
            name: "help",
            component: () => import( /* webpackChunkName: "help" */ "./views/help/HelpCenter.vue"),
        },
        // ======= Evaluation =======
        {
            path: "/evaluation/:slug/entry",
            name: "evaluation-entry",
            component: () => import( /* webpackChunkName: "evaluation-entry" */ "./views/evaluation/EvaluationEntry.vue"),
            meta: {requiresAuth: true}
        },
        {
            path: "/projects/:slug/evaluation",
            name: "evaluation-detail",
            component: () => import( /* webpackChunkName: "evaluation-detail" */ "./views/evaluation/EvaluationDetail.vue"),
            meta: {requiresAuth: true}
        },
        // ======= ACCOUNT =======
        {
            path: "/account/:slug?",
            name: "account",
            component: () => import( /* webpackChunkName: "account" */ "./views/account/Account.vue")
        },
        // ======= ADMINISTRATION =======
        {
            path: "/administration",
            name: "administration",
            component: () => import( /* webpackChunkName: "administration" */ "./views/admin/Administration.vue"),
            meta: {requiresAuth: true}
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