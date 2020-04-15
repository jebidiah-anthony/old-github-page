find ./ -name "*.adoc" 2>/dev/null | sed -e 's/\(.*\)adoc/rm \1html 2>\/dev\/null/g' > ./build_jekyll.sh

sh ./build_jekyll.sh

bundle exec jekyll build

find ./ -name "*.adoc" 2>/dev/null | sed -e 's/.\/\(.*\).adoc/mv _site\/\1.html .\/\1.html/g' > ./build_jekyll.sh

sh ./build_jekyll.sh

rm ./build_jekyll.sh
rm -rf _site/
rm -rf .jekyll-cache/
