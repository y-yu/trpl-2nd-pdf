FROM frolvlad/alpine-glibc:alpine-3.7

MAINTAINER yyu <yyu [at] mental.poker>

ENV TEXLIVE_DEPS \
    xz \
    tar \
    fontconfig-dev
    
ENV TEXLIVE_PATH /usr/local/texlive

ENV PANDOC_DEPS \
    alpine-sdk \
    coreutils \
    ghc \
    gmp \
    libffi \
    linux-headers \
    musl-dev \
    zlib-dev \
    cabal \
    tar

ENV FONT_DEPS \
    unzip \
    fontconfig-dev

ENV FONT_PATH /usr/share/fonts/

ENV PERSISTENT_DEPS \
    python3 \
    wget \
    make \
    perl \
    ghostscript \
    inkscape \
    bash \
    git

ENV PANDOC_VERSION 2.1.3
ENV PANDOC_DOWNLOAD_URL https://hackage.haskell.org/package/pandoc-$PANDOC_VERSION/pandoc-$PANDOC_VERSION.tar.gz
ENV PANDOC_ROOT /usr/local/pandoc

ENV PATH $TEXLIVE_PATH/bin/x86_64-linuxmusl:$PANDOC_ROOT/bin:$PATH

RUN apk upgrade --update

# Install basic dependencies
RUN apk add --no-cache --virtual .persistent-deps $PERSISTENT_DEPS

# Setup fonts
RUN mkdir -p $FONT_PATH && \
    apk add --no-cache --virtual .font-deps $FONT_DEPS && \
    # Noto Serif
    wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSerif-unhinted.zip && \
      unzip -d NotoSerif-unhinted NotoSerif-unhinted.zip && \
      cp NotoSerif-unhinted/*.ttf $FONT_PATH && \
      rm -rf NotoSerif-unhinted.zip NotoSerif-unhinted && \
    # Noto Naskh Arabic
    wget https://noto-website-2.storage.googleapis.com/pkgs/NotoNaskhArabic-unhinted.zip && \
      unzip -d NotoNaskhArabic-unhinted NotoNaskhArabic-unhinted.zip && \
      cp NotoNaskhArabic-unhinted/*.ttf $FONT_PATH && \
      rm -rf NotoNaskhArabic-unhinted.zip NotoNaskhArabic-unhinted && \
    # Noto Serif CJK JP
    wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSerifCJKjp-hinted.zip && \
      unzip -d NotoSerifCJKjp-hinted NotoSerifCJKjp-hinted.zip && \
      cp NotoSerifCJKjp-hinted/*.otf $FONT_PATH && \
      rm -rf NotoSerifCJKjp-hinted.zip NotoSerifCJKjp-hinted && \
    # Noto Sans Devanagari
    wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSansDevanagari-unhinted.zip && \
      unzip -d NotoSansDevanagari-unhinted NotoSansDevanagari-unhinted.zip && \
      cp NotoSansDevanagari-unhinted/*.ttf $FONT_PATH && \
      rm -rf NotoSansDevanagari-unhinted.zip NotoSansDevanagari-unhinted && \
    # Noto Emoji
    wget https://noto-website-2.storage.googleapis.com/pkgs/NotoEmoji-unhinted.zip && \
      unzip -d NotoEmoji-unhinted NotoEmoji-unhinted.zip && \
      cp NotoEmoji-unhinted/*.ttf $FONT_PATH && \
      rm -rf NotoEmoji-unhinted.zip  NotoEmoji-unhinted && \
    # Noto Sans Hebrew
    wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSansHebrew-unhinted.zip && \
      unzip -d NotoSansHebrew-unhinted NotoSansHebrew-unhinted.zip && \
      cp NotoSansHebrew-unhinted/*.ttf $FONT_PATH && \
      rm -rf NotoSansHebrew-unhinted.zip NotoSansHebrew-unhinted && \
    # Source Code Pro
    wget https://github.com/adobe-fonts/source-code-pro/archive/2.030R-ro/1.050R-it.zip && \
      unzip 1.050R-it.zip && \
      cp source-code-pro-2.030R-ro-1.050R-it/OTF/*.otf $FONT_PATH && \
      rm -rf 1.050R-it.zip source-code-pro-2.030R-ro-1.050R-it && \
    fc-cache -f -v && \
    apk del .font-deps 

# Install Pandoc
# See https://github.com/skyzyx/alpine-pandoc/blob/master/Dockerfile
RUN apk add --no-cache --virtual .pandoc-deps $PANDOC_DEPS  && \
    apk add --no-cache --virtual .cabal cabal -X http://dl-cdn.alpinelinux.org/alpine/edge/community && \
    wget -qO- "$PANDOC_DOWNLOAD_URL" | tar -xzf - && \
      ( cd pandoc-$PANDOC_VERSION && cabal update && cabal install --only-dependencies && \
      cabal configure --prefix=$PANDOC_ROOT && \
      cabal build && \
      cabal copy && \
      cd .. ) && \
    rm -Rf pandoc-$PANDOC_VERSION/ && \
    rm -Rf /root/.cabal/ /root/.ghc/ && \
    apk del .pandoc-deps .cabal

# Install Pandocfilter
COPY requirements.txt ./
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    rm requirements.txt

# Install TeXLive
RUN apk add --no-cache --virtual .texlive-deps $TEXLIVE_DEPS && \
    mkdir /tmp/install-tl-unx && \
    wget -qO- http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz | \
      tar -xz -C /tmp/install-tl-unx --strip-components=1 && \
    printf "%s\n" \
      "TEXDIR $TEXLIVE_PATH" \
      "selected_scheme scheme-small" \
      "option_doc 0" \
      "option_src 0" \
      > /tmp/install-tl-unx/texlive.profile && \
    /tmp/install-tl-unx/install-tl \
      -profile /tmp/install-tl-unx/texlive.profile && \
    tlmgr install latexmk collection-luatex collection-langjapanese \
      collection-fontsrecommended type1cm mdframed needspace fncychap \
      everyhook svn-prov enumitem background everypage && \
    rm -fr /tmp/install-tl-unx && \
    apk del .texlive-deps

VOLUME ["/workdir"]

WORKDIR /workdir

ENTRYPOINT ["/bin/bash", "-c", "./setup.sh && make"]
