import { stringify } from 'qs';
import request from '@/utils/request';


export async function queryTabs() {
  return request('/api/tag');
}

export async function queryCardsList(params) {
  return request(`/api/tag/${params.id}/cards`);
}

export async function searchCardsList(params) {
  return request(`/api/card/search?${stringify(params)}`);
}

export async function searchCollectCardsList(params) {
  return request(`/api/card/collect?${stringify(params)}`);
}
