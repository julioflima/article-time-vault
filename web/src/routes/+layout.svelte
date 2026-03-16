<script lang="ts">
  import type { Snippet } from "svelte";
  import { assets, base } from "$app/paths";
  import "$lib/styles/global.scss";

  let { children }: { children: Snippet } = $props();
  const utopiaStyle = `--utopia-image: url('${assets}/utopia.png')`;
</script>

<nav class="site-nav">
  <a href="{base}/" class="site-nav__brand"></a>
  <div class="site-nav__links">
    <a href="{base}/">Secret</a>
    <a href="{base}/decrypt">Reveal</a>
    <a href="{base}/article">Article</a>
    <a href="{base}/whitepaper.pdf" target="_blank" rel="noopener">Whitepaper</a
    >
  </div>
</nav>

<div class="bg-ambient" style={utopiaStyle}></div>
<div class="bg-image" style={utopiaStyle}></div>
<div class="page-content">
  {@render children()}
</div>

<style lang="scss">
  @use "$lib/styles/variables" as *;

  .site-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.5rem;
    border-radius: 0;
    border-top: none;
    border-left: none;
    border-right: none;
  }

  .site-nav__brand {
    font-family: $font-brand;
    font-size: 1.25rem;
    font-weight: 400;
    color: $color-black;
    text-decoration: none;
  }

  .site-nav__links {
    display: flex;
    gap: 1.5rem;

    a {
      font-size: 0.85rem;
      font-weight: 500;
      color: $color-black-80;
      text-decoration: none;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      transition: color $transition-fast;

      &:hover {
        color: $color-black;
      }
    }
  }

  .page-content {
    position: relative;
    z-index: 2;
  }
</style>
