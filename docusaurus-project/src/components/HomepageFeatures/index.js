import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'ROS 2 Fundamentals',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Master the Robot Operating System 2 for building distributed robotic applications.
        Learn nodes, topics, services, actions, and launch systems with hands-on exercises.
      </>
    ),
  },
  {
    title: 'Digital Twin & Simulation',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Create realistic simulations using Gazebo, Unity, and NVIDIA Isaac Sim.
        Bridge the gap between virtual prototyping and real-world deployment.
      </>
    ),
  },
  {
    title: 'VLA & Humanoid Systems',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Implement Vision-Language-Action models for natural robot interaction.
        Design complete humanoid systems with locomotion, manipulation, and conversational AI.
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
        <Heading as="h3">{title}</Heading>
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
