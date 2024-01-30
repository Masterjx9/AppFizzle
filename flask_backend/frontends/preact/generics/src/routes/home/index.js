import { h } from 'preact';
import style from './style.css';

const Home = () => {
	const handleClick = () => {
        alert('Hello from AppFizzle!');
    };

	return (
		<div class={style.home}>
			<a href="https://preactjs.com">
				<img src="../../assets/preact-logo.svg" alt="Preact Logo" height="160" width="160" />
			</a>
			<h1>Welcome to AppFizzle!</h1>
    		<p>This is a basic preact application.</p>
			<h3>Get Started Building PWAs with Preact-CLI</h3>
			<section class={style.clickMeSection}>
                <div onClick={handleClick} class={style.resource} style={{ cursor: 'pointer' }}>
                    <h2>Click Me</h2>
                    <p>Click to see a greeting from AppFizzle!</p>
                </div>
            </section>

			<section class={style.resourcesSection}>
				<Resource
					title="Learn Preact"
					description="If you're new to Preact, try the interactive tutorial to learn important concepts"
					link="https://preactjs.com/tutorial/"
				/>
				<Resource
					title="Differences to React"
					description="If you're coming from React, check out our docs for where Preact differs"
					link="https://preactjs.com/guide/v10/differences-to-react"
				/>
				<Resource
					title="Learn Preact-CLI"
					description="To learn more about Preact-CLI, read through the ReadMe & Wiki"
					link="https://github.com/preactjs/preact-cli#preact-cli--"
				/>
			</section>
		</div>
	);
};

const Resource = props => {
	return (
		<a href={props.link} class={style.resource}>
			<h2>{props.title}</h2>
			<p>{props.description}</p>
		</a>
	);
};

export default Home;
