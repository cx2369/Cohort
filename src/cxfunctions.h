#include <stddef.h>
#include <stdint.h>

#ifndef CXFUNCTIONS_H_
#define CXFUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif
    int test1();
    void cx_init(char *target_path);
    uint8_t __attribute__((hot)) cx_has_new_bits(uint8_t *cx_trace_bits);
    void update_after_new_edge(uint8_t *virgin_bits);
    void cx_delete_after_new_edge();
    void cx_write_solved_id_to_file();
    void cx_write_useless_edge_id_to_file();
    void cx_delete_cur_HNodeInfoRuns();
    void cx_set_afl_final_loc(uint32_t num);
    void cx_update_edge_time(uint8_t *virgin_bits_for_edge_time, uint8_t *virgin);
    void cx_set_cur_edge_useless();
    uint32_t cx_should_recompile();
    void cx_update_afl_useless_id();
    void cx_update_cx_useless_id();
    void cx_update_cxqueueid_hnoderuninfos(uint8_t *cx_trace_bits, uint32_t cx_queue_id);
    void cx_set_cur_cxid_and_hnodeinforuns(uint8_t *cx_trace_bits, uint32_t cx_queue_id);
    void cx_hnodeinforuns_bak_clear();
    void cx_hnodeinforuns_bak_bak();
    uint8_t cx_cxqueueid_cov_all_hnode(uint32_t cxid);
    uint8_t cx_cxqueueid_cov_better_progress(uint32_t cxid);
    uint8_t cx_cxqueueid_cov_all_state(uint32_t cxid);
    uint8_t cx_cxqueueid_cov_all_hash(uint32_t cxid);
    void cx_delete_cxqueueid_hnoderuninfos_with_id(uint32_t cxid);
    void cxqueueid_hnodeinforuns_bak_clear();
    void cxqueueid_hnodeinforuns_bak_bak(uint32_t cxid);
    void cx_set_queue_hnodeinfo_for_trim(uint8_t *cx_trace_bits);
    uint64_t cx_get_hnodeinfo_cksum(uint8_t *cx_trace_bits);
    void cx_hnodeid_hnodeinforunbak_clear();
    void cx_hnodeid_hnodeinforunbak_bak();
    void cx_set_label1(uint8_t num);
    void cx_set_cur_mut_loc(uint32_t num);
    void cx_update_cxid_hnodeids(uint8_t *cx_trace_bits, uint32_t cx_queue_id);
    void cx_update_aflid_hnodeids(uint8_t *cx_trace_bits, uint32_t afl_queue_id);
    void cx_delete_cxid_hnodeids_with_id(uint32_t cxid);
    void cx_delete_cxid_edgeid_fuzzcount_with_id(uint32_t cxid);
    void cx_clear_cur_mut_locs();
    void cx_reset_cur_mut_locs(uint8_t afl_or_cx, uint32_t queue_id, uint32_t queue_len);
    uint32_t cx_get_cur_mut_locs_size();
    uint32_t cx_get_random_in_cur_mut_locs();
    void cx_update_hnode_fuzzed_count(uint8_t afl_or_cx, uint32_t queue_id);
    uint32_t cx_get_smaller_fuzzed_hnodeid();
    uint8_t cx_queue_reach_this_hnodeid(uint32_t cxid, uint32_t hnodeid);
    void cx_update_for_has_queue_not_fuzzed(uint32_t cxid);
    void cx_clear_has_queue_not_fuzzed();
    void cx_update_has_queue_not_fuzzed();
    void cx_update_queueid_edgeid(uint8_t afl_or_cx, uint32_t queue_id, uint8_t *trace_bits, uint32_t trace_bytes);
    void cx_update_edgeid_fuzzcount(uint8_t afl_or_cx, uint32_t queue_id);
    void cx_bak_hnodeids();
    void cx_set_cov_all_state_cxid();
    void cx_set_cov_all_hash_cxid();
    void cx_set_cov_all_better_progress_cxid();
    void cx_clear_fuzzed_cxid();
    void cx_update_fuzzed_cxid(uint32_t cxid);
    void cx_update_has_hnode_cov_not_fuzzed();
    void cx_update_hnodeinforuns_bestcxid(uint32_t cxid, uint64_t factor);
    void cx_set_edge_count_best_cxid();
    void cx_set_cur_edge_count(uint8_t *trace_bits);
    void cx_update_edge_count_best_cxid(uint32_t cxid, uint64_t factor);
    void cx_set_cov_all_edge_count_cxid(uint8_t *virgin_bits);
    uint8_t cx_cxqueueid_cov_all_edge_count(uint32_t cxid);
    void cx_set_edge_id_fuzz_count();
#ifdef __cplusplus
}
#endif //  __cplusplus end

#endif // CXFUNCTIONS_H_ end
