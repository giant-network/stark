import React, { PureComponent } from 'react';
import Link from 'umi/link';
import RightContent from '../GlobalHeader/RightContent';
import { getFlatMenuKeys } from '../SiderMenu/SiderMenuUtils';
import styles from './index.less';
import { title } from '../../defaultSettings';

export default class TopNavHeader extends PureComponent {
  render() {
    const { theme, contentWidth, logo, siteHeader } = this.props;
    
    return (
      <div className={`${styles.head} ${theme === 'light' ? styles.light : ''}`}>
        <div
          ref={ref => {
            this.maim = ref;
          }}
          className={`${styles.main} ${contentWidth === 'Fixed' ? styles.wide : ''}`}
        >
          <div className={styles.left}>
            <div className={styles.logo} key="logo">
              <Link to="/">
                <img src={logo} alt="logo" />
                <h1>{siteHeader || title}</h1>
              </Link>
            </div>
          </div>
          <RightContent {...this.props} />
        </div>
      </div>
    );
  }
}
