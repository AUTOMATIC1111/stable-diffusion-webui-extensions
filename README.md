# This is the Extension Index of Stable Diffusion Web UI

[Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) downloads `index.json` from this repo to show user the list of available extensions.

## How to submit extension

If you wish to add an extension to the index, make an entry in `extensions directory` using `extension_template.json`, write a short extension description and tag the extension appropriately, then open as a pull request ty!

## Tags

A list of available `tags` can be found at the top of index.json

- `online` tag is **Required** for any extension that connections to external server during regular use aside from one time downloading of assets.

- `ads` tag is **Required** for any extension that contains advertisements or self-advertisement in the extension itself.

- `localization` tag is for localization files only, not for extension that adds localization functionalities such as translator.

- `installed` tag it is used internally by webui and not to be used for extension categorization.

## Notes

- An extension will need to be functioning for it to be included.

- If extension is no longer functional and not maintained, we might redirect it to a fork or remove it form the index.

- Not all extensions will be accepted, we will review the extension and make an assessment.

- Even if you're not the author of the extension, you can submit the extension for them.

- If you wish to have your extension removed, or believes the description does not properly describe your extension, please open the issue or pull request.
