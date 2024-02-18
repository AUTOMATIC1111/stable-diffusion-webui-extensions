# This is the Extension Index of Stable Diffusion Web UI

[Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) accesses [`index.json`](https://github.com/AUTOMATIC1111/stable-diffusion-webui-extensions/blob/master/index.json) from this repo to show user the list of available extensions.

## How to submit extension

If you wish to add an extension onto the index, make an entry in `extensions` directory using `extension_template.json`, write a short description and tag it appropriately then open as a pull request ty!

### Step by step instructions

1. Fork of this repository.

2. Make a copy of `extension_template.json`

3. Fill in the copy and rename it appropriately

4. Move it into `extensions` directory 

5. Submit a pull request and wait for review.

- Extensions pull requests targets [`extensions branch`](https://github.com/AUTOMATIC1111/stable-diffusion-webui-extensions/tree/extensions), after merge it is automatically assembled and deployed to [`master branch`](https://github.com/AUTOMATIC1111/stable-diffusion-webui-extensions/tree/master) using GitHub Actions.

- Don't edit the `index.json` directly and don't modify any other files unless you have a special reason.

- The `added` date will be automatically populated after merge.

## Tags

A list of available `tags` and their description can be found at in `tags.json`

- `online` tag is **Required** for any extension that connections to external server during regular use aside from one time downloading of assets.

- `ads` tag is **Required** for any extension that contains advertisements or self-advertisement in the extension itself.

- `localization` tag is for localization files only, not for extension that adds localization functionalities such as translator.

- `installed` tag it is used internally by webui, it is not meant to be used for extension categorization.

## Notes

- An extension will need to be functioning for it to be included.

- If extension is no longer functional and or not maintained, we might redirect it to a fork or remove it from the index.

- Not all extensions will be accepted, we will review the extension and make an assessment.

- You can submit extensions even if you are not the author, but it is preferred that the author do it themselves.

- If you wish to have your extension removed, or believes the description does not properly describe your extension, please open the issue or pull request.
