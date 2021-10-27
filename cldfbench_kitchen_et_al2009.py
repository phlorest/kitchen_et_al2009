import pathlib

import nexus
import phlorest


def fix_nexus(p):
    if not isinstance(p, str):
        p = p.read_text(encoding='utf8')
    return p.replace('.Arabic', '_Arabic')


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "kitchen_et_al2009"

    def cmd_makecldf(self, args):
        self.init(args)
        with self.nexus_summary() as nex:
            self.add_tree_from_nexus(
                args,
                nexus.NexusReader.from_string(fix_nexus(self.raw_dir / 'kitchen2009.mcct.trees')),
                nex,
                'summary',
                detranslate=True,
            )
        posterior = self.sample(
            self.remove_burnin(
                fix_nexus(self.read_gzipped_text(self.raw_dir / 'Semitic.Greenhill.trees.gz')),
                200),
            detranslate=True,
            as_nexus=True)

        with self.nexus_posterior() as nex:
            for i, tree in enumerate(posterior.trees.trees, start=1):
                self.add_tree(args, tree, nex, 'posterior-{}'.format(i))

        self.add_data(
            args,
            nexus.NexusReader.from_string(fix_nexus(self.raw_dir / 'kitchen_et_al2009-Binary.nex')))
