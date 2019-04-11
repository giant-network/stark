export default [
  // app
  {
    path: '/',
    component: '../layouts/BasicLayout',
    Routes: ['src/pages/Authorized'],
    routes: [
      // dashboard
      { path: '/',
        name: 'dashboard',
        hideInMenu: true,
        component: './Dashboard/HomePage',
      },
      {
        component: '404',
      },
    ],
  },
];
