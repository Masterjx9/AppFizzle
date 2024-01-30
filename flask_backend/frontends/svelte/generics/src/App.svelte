<script>
  // JavaScript part
	export let name;

  function handleClick() {
    alert('Hello from AppFizzle!');
  }
</script>

<main>
	<h1>Welcome to {name}!</h1>
<p>This is a basic Svelte application.</p>
<button on:click={handleClick}>Click Me</button>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>