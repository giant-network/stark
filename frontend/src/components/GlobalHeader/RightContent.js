import React, { PureComponent } from 'react';
import SelectLang from '../SelectLang';
import styles from './index.less';
import HeaderSearch from '../HeaderSearch';
import { connect } from 'dva';


@connect(({ list, loading }) => ({
  list,
  loading: loading.models.list,
}))
export default class GlobalHeaderRight extends PureComponent {
  searchCard = (value) => {
    const { dispatch } = this.props;

    dispatch({
      type: 'list/fetchCardsList',
      payload: {'q': value}
    }).then(
      () => {
        const { list: { searchCardsList, cardsList } } = this.props;
        dispatch({
            type: "list/pushCards",
            payload: {cards: searchCardsList, 'name': 'searchCard'}
        })
      }
    );
  };

  render() {
    const {
      theme,
    } = this.props;

    let className = styles.right;
    if (theme === 'dark') {
      className = `${styles.right}  ${styles.dark}`;
    }

    return (
      <div className={className}>
        <HeaderSearch
          className={`${styles.action} ${styles.search}`}
          placeholder="站内搜索"
          onPressEnter={value => {
            this.searchCard(value); // eslint-disable-line
          }}
          defaultOpen={true}
          open={true}
        />
        {/*<SelectLang className={styles.action} />*/}
      </div>
    );
  }
}
