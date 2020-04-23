import dva from 'dva';
import createLoading from 'dva-loading';

const runtimeDva = window.g_plugins.mergeConfig('dva');
let app = dva({
  history: window.g_history,
  
  ...(runtimeDva.config || {}),
});

window.g_app = app;
app.use(createLoading());
(runtimeDva.plugins || []).forEach(plugin => {
  app.use(plugin);
});

app.model({ namespace: 'global', ...(require('/Users/felix/3myproject/stark/frontend/src/models/global.js').default) });
app.model({ namespace: 'list', ...(require('/Users/felix/3myproject/stark/frontend/src/models/list.js').default) });
app.model({ namespace: 'menu', ...(require('/Users/felix/3myproject/stark/frontend/src/models/menu.js').default) });
app.model({ namespace: 'setting', ...(require('/Users/felix/3myproject/stark/frontend/src/models/setting.js').default) });
