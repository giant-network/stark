import { queryCardsList, queryTabs, searchCardsList, searchCollectCardsList } from '@/services/api';

export default {
  namespace: 'list',

  state: {
    cardsList: {
      cards: []
    },
    tabsList: [],
  },

  effects: {
    *fetch({ payload }, { call, put }) {
      const response = yield call(queryCardsList, payload);
      yield put({
        type: 'queryList',
        payload: response,
      });
    },
    *fetchTabs({ payload }, { call, put }) {
      const response = yield call(queryTabs, payload);
      yield put({
        type: 'queryTabsList',
        payload: Array.isArray(response) ? response : [],
      });
    },
    *fetchCardsList({ payload }, { call, put }) {
      const response = yield call(searchCardsList, payload);
      yield put({
        type: 'searchCardsRes',
        payload: response,
      });
    },
    *pushCards({ payload }, { call, put }) {
      yield put({
        type: 'queryList',
        payload: payload,
      });
    },
    *fetchCollectedCardsList({ payload }, { call, put }) {
      const response = yield call(searchCollectCardsList, payload);
      yield put({
        type: 'queryList',
        payload: {cards: response},
      });
    },
    *reloadCards({ payload }, { call, put }) {
      yield put({
        type: 'queryList',
        payload: payload,
      });
    },
  },

  reducers: {
    queryList(state, action) {
      return {
        ...state,
        cardsList: action.payload,
      };
    },
    queryTabsList(state, action) {
      return {
        ...state,
        tabsList: action.payload,
      };
    },
    searchCardsRes(state, action) {
      return {
        ...state,
        searchCardsList: action.payload,
      };
    },
  },
};
