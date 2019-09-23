Event
* Create check suite
* Create general check run

|
V

Checkout
* Pull git repo, tarball, store in object store (s3)

|
V

Analysis (Determine package details, build type)
* Safe/static analysis

|
| Python+{PEP517,setuptools} only
V

Initial build 
* Linux+amd64+Py3
* sdist, bdist

|
V

Finish analysis
* Pure or binary
* Py2 status

|
V

Additional builds
* bdist
* Windows+amd64, Mac+amd64 (future)
* Linux+Arm (future?)
* Py2

|
V

(mutliplex) running test suite (future)

|
V

Upload
* If all builds succeeded and all tests succeeded
* Mainline: If "dev" version, upload to test.pypi
* PR: No upload
* Prerelease (by version number or GitHub checkbox): Upload to GitHub, test.pypi, pypi
* Full release: Upload to GitHub, test.pypi, pypi



aurynn:
okay so if you trust your code for uploading and all your stuff is in consistent places then I'd say that your sidecar can probably operate as a shared filesystem with the untrusted container, mapping /dist, and upload stuff from there to S3

sidecar implements download, upload, and splunk logging interface. Output: buffer and upload through the artifact channel.


Webhook (HTTP+Lambda): Accept github event, setup check suite, trigger checkout+analysis

Checkout (Direct ECS execution): Checkout repo, run static analysis, trigger build

Build (Direct ECS execution):
* /project: Cross-mount
* Primary Container: Run build
* Sidecar: Pull checkout, proxy logs (splunk api) to github, push artifacts
* Has extremely limited ephemeral IAM Role

S3 trigger (Lambda): Pull artifacts, upload to repos

Cron: Scan AWS account for expired ephemeral resources, destroy them

Splunk API: http://dev.splunk.com/view/event-collector/SP-CAAAE7H
