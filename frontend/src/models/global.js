import { queryTabs} from '@/services/api';

export default {
  namespace: 'global',

  state: {
    collapsed: false,
    notices: [],
  },

  effects: {
    *fetchNotices({ payload }, { call, put }) {
      const data = yield call(queryTabs);
      yield put({
        type: 'saveNotices',
        payload: data,
      });
    },
  },

  reducers: {
    saveNotices(state, { payload }) {
      return {
        ...state,
        notices: payload,
      };
    },
  },
};
