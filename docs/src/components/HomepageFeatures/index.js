import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'File validation based on MIME',
    Svg: require('@site/static/img/file-mimes.svg').default,
    description: (
      <>
        You can validate files based on <code>MIME</code>  and their <code>magic numbers</code> using the File Validator library
      </>
    ),
  },
  {
    title: 'File Size Validation',
    Svg: require('@site/static/img/check.svg').default,
    description: (
      <>
        In addition to the validation of files based on MIME and ... you can also validate files by size.
      </>
    ),
  },
  {
    title: 'Support for django',
    Svg: require('@site/static/img/django.svg').default,
    description: (
      <>
        Provide <b>ValidatedFilefield</b> and <b>FileValidator</b> for file validation in Django
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
