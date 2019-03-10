import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import Error404 from "./views/error/404.vue";
import store from "./store";

Vue.use(Router);

export const USE_REQUIRED_AUTH = process.env.VUE_APP_FORCE_LOGIN == "true"

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: "/login",
            name: "login",
            component: Login,
            meta: { public: true }
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
            path: "/projects/:id",
            name: "project-detail",
            component: () => import( /* webpackChunkName: "project-detail" */ "./views/project/Detail.vue")
        },
        {
            path: "/projects/:id/manage",
            name: "project-manage",
            component: () => import( /* webpackChunkName: "project-manage" */ "./views/project/Manage.vue")
        },
        // ======= ACCOUNT =======
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

/* Configure forced login behavior here */
if (USE_REQUIRED_AUTH) {
    router.beforeEach((to, from, next) => {
        if (!to.matched.some(record => record.meta.public)) {
            // this route requires auth, check if logged in
            // if not, redirect to login page.
            if (!store.getters['user/isLoggedIn']) {
                console.log("Auth not found, Forcing login")
                next({
                    path: '/login',
                    query: { redirect: to.fullPath }
                })
            } else {
                next()
            }
        } else {
            next() // make sure to always call next()!
        }
    })
}

export default router;