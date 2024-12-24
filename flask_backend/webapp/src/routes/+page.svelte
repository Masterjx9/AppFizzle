<script lang="ts">
    import { onMount } from 'svelte';

    // Reactive variables for selected frontend and backend
    let frontend: string = '';
    let backend: string = '';

    // State for managing download link visibility
    let isDownloadReady: boolean = false;
    let downloadUrl: string = '';

    // Function to handle form submission
    const handleSubmit = async (event: Event) => {
        event.preventDefault();
        isDownloadReady = false;

        try {
            const response = await fetch('http://localhost:5000/builder_dockerpackage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ frontend, backend }),
            });

            if (!response.ok) {
                throw new Error('Failed to download file');
            }

            const blob = await response.blob();
            downloadUrl = URL.createObjectURL(blob);
            isDownloadReady = true;
        } catch (error) {
            console.error('Error:', error);
        }
    };
</script>


<div class="container">
    <div class="card">
        <div class="card-header">Welcome to Appfizzle</div>
        <div class="card-body">
            <form on:submit|preventDefault={handleSubmit}>
                <div class="form-group">
                    <label for="frontendSelect">Select Frontend</label>
                    <select
                        class="form-control"
                        id="frontendSelect"
                        bind:value={frontend}
                        name="frontend"
                    >
                        <option value="alpinejs">alpinejs</option>
                        <option value="angular">angular</option>
                        <option value="aurelia">aurelia</option>
                        <option value="backbonejs">backbonejs</option>
                        <option value="ember">ember</option>
                        <option value="litelement">litelement</option>
                        <option value="mod.rs">mod.rs</option>
                        <option value="preact">preact</option>
                        <option value="react">react</option>
                        <option value="solid">solid</option>
                        <option value="stimulus">stimulus</option>
                        <option value="svelte">svelte</option>
                        <option value="vuejs">vuejs</option>
                        <option value="wasm_blazor">wasm_blazor</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="backendSelect">Select Backend</label>
                    <select
                        class="form-control"
                        id="backendSelect"
                        bind:value={backend}
                        name="backend"
                    >
                        <option value="adonis">adonis</option>
                        <option value="akka-http">akka-http</option>
                        <option value="asp_net_core">asp_net_core</option>
                        <option value="blazor">blazor</option>
                        <option value="codeigniter">codeigniter</option>
                        <option value="coldfusion">coldfusion</option>
                        <option value="cowboy">cowboy</option>
                        <option value="dancer">dancer</option>
                        <option value="django">django</option>
                        <option value="flask">flask</option>
                        <option value="go">go</option>
                        <option value="ktor">ktor</option>
                        <option value="laravel">laravel</option>
                        <option value="meteorjs">meteorjs</option>
                        <option value="micronaut">micronaut</option>
                        <option value="mod.rs">mod.rs</option>
                        <option value="nodejs">nodejs</option>
                        <option value="phoenix">phoenix</option>
                        <option value="play-framework">play-framework</option>
                        <option value="quarkus">quarkus</option>
                        <option value="ruby-on-rails">ruby-on-rails</option>
                        <option value="shiny">shiny</option>
                        <option value="sinatra">sinatra</option>
                        <option value="spring-boot">spring-boot</option>
                        <option value="symfony">symfony</option>
                        <option value="yesod">yesod</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-custom btn-block">
                    Create Dockerfile
                </button>
            </form>
            {#if isDownloadReady}
                <a href={downloadUrl} download="dockerfile_package.zip">Download File</a>
            {/if}
        </div>
    </div>
</div>
