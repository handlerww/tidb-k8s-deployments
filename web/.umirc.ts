import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  routes: [
    { path: '/', title:'TiDB Cluster Manager', component: '@/pages/index' },
  ],
});
